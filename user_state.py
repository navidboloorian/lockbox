class UserState:
  private_key = None

  @classmethod
  def set_private_key(cls, private_key):
    cls.private_key = private_key