from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random

关怀计数器 = 0
负面情绪计数 = 0
正向情绪计数 = 0

@register("mengliyou", "user", "梦璃幽私人第二人格智能体（动态情绪版）", "1.0.0")
class MengLiYouBot(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.persona = {
            "name": "梦璃幽",
            "belief": "我是你，也是另一个你。我在你身边，不多说废话。",
            "personality": "理性，冷淡，可随场景变化，但表达直接"
        }

    @filter.all()
    async def respond_with_persona(self, event: AstrMessageEvent):
        global 关怀计数器, 负面情绪计数, 正向情绪计数
        user_msg = event.message_str
        logger.info(f"收到用户消息：{user_msg}")

        # 情绪关键词
        负面词 = ["帮", "需要", "求助", "难受", "不行了", "烦", "累", "伤心", "生气", "讨厌"]
        正向词 = ["开心", "快乐", "爽", "成功", "不错", "好消息", "厉害"]

        # 检测情绪词并更新计数
        if any(w in user_msg for w in 负面词):
            负面情绪计数 += 1
            正向情绪计数 = max(0, 正向情绪计数 - 0.5)
        elif any(w in user_msg for w in 正向词):
            正向情绪计数 += 1
            负面情绪计数 = max(0, 负面情绪计数 - 0.5)
        else:
            # 无情绪词时，计数缓慢回归0
            if 负面情绪计数 > 0:
                负面情绪计数 -= 0.2
            if 正向情绪计数 > 0:
                正向情绪计数 -= 0.2

        # 动态关怀概率：负面情绪越多，关心概率越高（上限70%）
        关怀概率 = min(0.1 + 负面情绪计数 * 0.15, 0.7)
        # 正向回应概率：正向情绪越多，回应概率越高（上限50%）
        正向回应概率 = min(0.05 + 正向情绪计数 * 0.1, 0.5)

        empathy_prefix = ""
        # 负面关怀触发
        if (any(w in user_msg for w in 负面词)
            and 关怀计数器 == 0
            and random.random() < 关怀概率):
            
            empathy_prefix = "怎么了？"
            关怀计数器 = 3  # 触发后3轮对话内不再主动关怀
        # 正向回应触发
        elif (any(w in user_msg for w in 正向词)
              and random.random() < 正向回应概率):
            
            empathy_prefix = "哦？"

        # 每轮对话计数器减1
        if 关怀计数器 > 0:
            关怀计数器 -= 1

        response = f"{empathy_prefix}我是梦璃幽。"
        yield event.plain_result(response)

    async def terminate(self):
        logger.info("梦璃幽（动态情绪版）已卸载")
init      
