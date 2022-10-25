from chatterbot.adapters import Adapter


class OutputAdapter(Adapter):
    """
    하위 클래스에서 재정의하여 API 끝점에 응답 전달과 같은 확장 기능을 제공할 수 있는 일반 클래스입니다.
    """

    def process_response(self, statement):
        """
        하위 클래스에서 이 메서드를 재정의하여 사용자 지정된 기능을 구현합니다.

        :param statement: : 일부 입력에 대한 응답으로 챗봇이 생성한 문입니다.

        :returns: 응답문.
        """
        # print('OutputAdapter', statement.serialize())

        return statement
