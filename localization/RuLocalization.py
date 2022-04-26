from bot_commands.EmbedUtils import ActionType
from data.models import StatisticType


class RuLocalization:
    @staticmethod
    def action_type_to_verb(action_type: ActionType) -> str:
        return {
            ActionType.ASKED: 'Запросил(а)',
            ActionType.EXECUTED: 'Выполнил(а)',
        }[action_type]

    @staticmethod
    def statistic_type_to_readable(statistic_type: StatisticType) -> str:
        return {
            StatisticType.BOT_COMMANDS_AMOUNT: 'Количество запросов к боту',
        }[statistic_type]




