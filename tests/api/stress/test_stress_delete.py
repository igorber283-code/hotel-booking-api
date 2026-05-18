import asyncio
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_booking_cancel_stress_load(ac: AsyncClient, test_room):
    """Стресс-тест: 50 одновременных запросов на отмену ОДНОЙ И ТОЙ ЖЕ брони.

    Система должна успешно отменить бронь только 1 раз.
    """
    # 1. Регистрируемся и логинимся
    user_data = {"email": "cancel_stress@example.com", "password": "Password123!"}
    await ac.post("/authx/register", json=user_data)
    login_res = await ac.post("/authx/login", json=user_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Создаем одну успешную бронь, которую будем мучить
    params = {"date_from": "2026-12-25", "date_to": "2026-12-30"}
    booking_res = await ac.post(
        f"/bookings/{test_room.id}", params=params, headers=headers
    )
    assert booking_res.status_code == 201
    booking_id = booking_res.json()["id"]  # Достаем ID созданной брони

    # 3. Функция для отправки DELETE запроса
    async def cancel_booking():
        # Меняй URL под свой роутер, например: /bookings/{id}
        return await ac.delete(f"/bookings/{booking_id}", headers=headers)

    # 4. Спамим 50 параллельных запросов на удаление
    tasks = [cancel_booking() for _ in range(50)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 5. Собираем статус-коды
    status_codes = [
        res.status_code for res in results if not isinstance(res, Exception)
    ]

    # Обычно успешное удаление возвращает 200 OK или 204 No Content
    success_count = status_codes.count(200) + status_codes.count(204)
    # Повторные запросы должны возвращать 404 (Not Found) или 400 (Bad Request)
    not_found_count = status_codes.count(404) or status_codes.count(400)
    other_errors = len(results) - success_count - not_found_count

    print("\n========== ИТОГИ СТРЕСС-ТЕСТА ОТМЕНЫ ==========")
    print(f"Успешно удалено (200/204): {success_count}")
    print(f"Уже удалено/Не найдено (404/400): {not_found_count}")
    print(f"Прочих ошибок/исключений: {other_errors}")

    # 6. Проверки (Ассерты)
    assert success_count == 1, (
        f"Бронь должна быть удалена ровно 1 раз, но удалилась {success_count} раз!"
    )
    assert success_count + not_found_count == 50, (
        "Сумма успешных ответов и 404 должна быть равна 50"
    )
