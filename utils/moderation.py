class moderation:
    def __init__(self,dictionary):
        self._goodWords = dictionary["goodWords"]
        self._badWords = dictionary["badWords"]

    def hasBadWords(self,msg):
        msgLowercase = msg.lower()
        for badWord in self._badWords:
            if badWord in msgLowercase:
                # bad word found
                return True
        return False

    def hasGoodWords(self,msg):
        msgLowercase = msg.lower()
        for goodWord in self._goodWords:
            if goodWord in msgLowercase:
                # good word found
                return True
        return False
