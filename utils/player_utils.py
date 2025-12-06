# utils/player_utils.py

from models import Player


def format_player_characteristics(player: Player) -> str:
    """
    Формирует и возвращает отформатированный текст с характеристиками игрока.
    
    Args:
        player: Объект игрока с характеристиками.
        
    Returns:
        Отформатированная строка с характеристиками игрока в HTML формате.
    """
    characteristics = player.characteristics
    if not characteristics:
        return "❗ У вас пока нет характеристик. Их выдадут в начале игры."

    return (
        f"<b>Ваши характеристики:</b>\n"
        f"👤 <b>Профессия:</b> {characteristics.profession}\n"
        f"🧬 <b>Биология:</b> {characteristics.biology}\n"
        f"❤️ <b>Здоровье:</b> {characteristics.health}\n"
        f"🎨 <b>Хобби:</b> {characteristics.hobby}\n"
        f"🎒 <b>Багаж:</b> {characteristics.luggage}\n"
        f"📜 <b>Факт:</b> {characteristics.facts}\n"
        f"😱 <b>Фобия:</b> {characteristics.phobia}\n"
        f"✨ <b>Талант:</b> {characteristics.talent}\n"
        f"🏷️ <b>Социальный статус:</b> {characteristics.social_status}"
    )
