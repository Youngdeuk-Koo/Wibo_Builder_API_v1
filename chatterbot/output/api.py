from chatterbot.output import OutputAdapter


class APIAdapter(OutputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_response(self, statement):
        """
        Print the response to the user's input.
        """
        statement.set_elapsed_time()
        return statement
