"""
OpenAI APIサービス
キャッチフレーズ生成（コスト最適化：3施設まとめて生成）
"""
from typing import List, Dict, Any
from openai import OpenAI
from api.core.config import settings


class OpenAIService:
    """OpenAI GPT-4o-miniを使用したキャッチフレーズ生成"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"  # 最安モデル

    async def generate_catchphrases(
        self,
        facilities: List[Dict[str, Any]],
        vibes: List[str],
        sensations: List[str],
    ) -> List[str]:
        """
        3施設分のキャッチフレーズを1回のAPI呼び出しで生成

        Args:
            facilities: 施設リスト（最大3件）
            vibes: ユーザーのVibe選択
            sensations: ユーザーのSensation選択

        Returns:
            キャッチフレーズのリスト（施設の順序と対応）
        """
        if not facilities or len(facilities) > 3:
            raise ValueError("施設は1-3件で指定してください")

        # プロンプト構築
        prompt = self._build_prompt(facilities, vibes, sensations)

        # OpenAI API呼び出し
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "あなたは日帰り温泉のキャッチコピーライターです。ユーザーの気分（Vibe/Sensation）に合わせて、施設の魅力を15文字以内で表現してください。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,  # クリエイティブに
            max_tokens=200,
        )

        # レスポンスパース
        catchphrases_text = response.choices[0].message.content.strip()
        catchphrases = self._parse_catchphrases(catchphrases_text, len(facilities))

        return catchphrases

    def _build_prompt(
        self,
        facilities: List[Dict[str, Any]],
        vibes: List[str],
        sensations: List[str],
    ) -> str:
        """
        プロンプト構築

        Args:
            facilities: 施設リスト
            vibes: Vibe選択
            sensations: Sensation選択

        Returns:
            プロンプト文字列
        """
        # Vibe/Sensationを日本語化
        vibe_map = {
            "forest": "森",
            "city": "都会",
            "snow": "雪",
            "bonfire": "焚き火",
            "hinoki": "檜",
            "concrete": "コンクリート",
            "ocean": "海",
            "cave": "洞窟",
            "morning": "朝",
            "sunset": "夕日",
            "solo": "一人",
            "party": "グループ",
        }
        vibes_ja = [vibe_map.get(v, v) for v in vibes]

        prompt = f"""ユーザーの気分:
Vibe: {', '.join(vibes_ja)}
Sensation: {', '.join(sensations)}

以下の温泉施設に対して、この気分に合う魅力的なキャッチフレーズを15文字以内で生成してください。

"""

        for i, facility in enumerate(facilities, 1):
            keywords = ", ".join(facility.get("keywords", [])[:5])  # 最初の5個
            prompt += f"""{i}. {facility['name']}
   住所: {facility['address']}
   料金: {facility['price']}円
   特徴: {keywords}

"""

        prompt += """各施設のキャッチフレーズを以下の形式で出力してください:
1. [キャッチフレーズ]
2. [キャッチフレーズ]
3. [キャッチフレーズ]

注意:
- 15文字以内
- ユーザーの気分（Vibe/Sensation）を反映
- 施設の特徴を活かす
- 魅力的で行きたくなる表現
"""

        return prompt

    def _parse_catchphrases(self, text: str, count: int) -> List[str]:
        """
        生成されたキャッチフレーズをパース

        Args:
            text: OpenAIのレスポンステキスト
            count: 施設数

        Returns:
            キャッチフレーズリスト
        """
        lines = text.strip().split("\n")
        catchphrases = []

        for line in lines:
            line = line.strip()
            # "1. キャッチフレーズ" 形式をパース
            if line and len(line) > 3 and line[0].isdigit():
                # 数字とピリオドを削除
                catchphrase = line.split(".", 1)[-1].strip()
                # 括弧も削除
                catchphrase = catchphrase.strip("[]【】「」")
                catchphrases.append(catchphrase)

        # 施設数と一致しない場合はデフォルト
        if len(catchphrases) != count:
            return ["温泉を楽しむ"] * count

        return catchphrases


# シングルトンインスタンス
openai_service = OpenAIService()
