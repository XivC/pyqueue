
class Task:

    def _execute(self):
        try:
            result = self.execute()
        except Exception as ex:
            self.on_error(ex)
        else:
            self.on_success(result)

    def execute(self):
        return None

    def on_success(self, result):
        pass

    def on_error(self, ex: Exception):
        pass