class Adapter(object):
    """
    모든 어댑터 클래스에 대한 슈퍼 클래스

    매개 변수 챗봇: 챗봇 인스턴스
    """

    def __init__(self, chatbot, **kwargs):
    
        self.chatbot = chatbot
        

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        어댑터 메서드가 구현되지 않은 경우 발생하는 예외
        일반적으로 이는 개발자가 하위 클래스에서 메소드를 구현해야 함을 나타냅니다
        """

        def __init__(self, message='하위 클래스 메서드에서 이 메서드를 재정의해야 합니다.'):
            """
            예외 메시지를 설정합니다.
            """
            super().__init__(message)

    class InvalidAdapterTypeException(Exception):                                                   # 12. 
        """
        예기치 않은 클래스 유형의 어댑터를 수신할 때 발생하는 예외입니다.
        """
        pass
