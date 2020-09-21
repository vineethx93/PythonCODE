
# For creating proper 'user' objects rather than dictionary


class User:
    # _id is used here since "id: is a keyword.. better to keep _id rather than any other name
    def __init__(self, _id, username, password):
        # DONOT change this "id" in "self.id" to any other name [JWT thing]
        self.id = _id
        self.username = username
        self.password = password
