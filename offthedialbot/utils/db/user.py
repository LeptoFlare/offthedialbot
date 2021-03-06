from offthedialbot import utils
from . import db, Tournament
from .signup import Signup


class User:
    """Represents what useUser would be."""

    col = db.collection(u"users")

    def __init__(self, id):
        self.id = str(id)
        self.doc = self.col.document(self.id).get()
        self.ref = self.doc.reference
        self.dict = self.doc.to_dict()
        self.tourney = Tournament()

    def signup(self, ignore_ended=False):
        """Return the possible user's signup (useSignup)."""
        if self.tourney.has_ended() and not ignore_ended:
            return None

        return Signup(self.id)

    def is_banned(self):
        return None

    async def smashgg(self):
        """Get smash.gg data from the api with the user slug."""
        query = """query($slug: String) {
          user(slug: $slug) {
            player {
              gamerTag
            }
          }
        }"""
        status, data = await utils.graphql("smashgg", query, {"slug": self.dict["profile"]["smashgg"]})
        return data["data"]["user"]

    async def discord(self, bot):
        user = bot.get_user(self.id)
        if not user:
            user = await bot.fetch_user(self.id)
        return user

    def get_elo(self):
        return sum([self.rank_to_power(rank) for rank in self.get_ranks()]) / 4

    def get_playstyles(self, type=None):
        try:
            if type:
                return self.dict["profile"]["stylepoints"][type]
            else:
                return [
                    self.dict["profile"]["stylepoints"]["support"],
                    self.dict["profile"]["stylepoints"]["aggressive"],
                    self.dict["profile"]["stylepoints"]["objective"],
                    self.dict["profile"]["stylepoints"]["slayer"],
                    self.dict["profile"]["stylepoints"]["anchor"],
                    self.dict["profile"]["stylepoints"]["mobile"],
                    self.dict["profile"]["stylepoints"]["flex"],
                    self.dict["profile"]["stylepoints"]["focused"],
                ]
        except KeyError:
            return None

    def get_ranks(self):
        try:
            return [
                self.dict["profile"]["ranks"]["sz"],
                self.dict["profile"]["ranks"]["tc"],
                self.dict["profile"]["ranks"]["rm"],
                self.dict["profile"]["ranks"]["cb"],
            ]
        except KeyError:
            return None

    @staticmethod
    def rank_to_power(rank):
        if rank.startswith("X"):
            return float(rank[1:])
        return {
            "C-": 1000,
            "C": 1100,
            "C+": 1200,
            "B-": 1250,
            "B": 1450,
            "B+": 1550,
            "A-": 1650,
            "A": 1700,
            "A+": 1800,
            "S": 1900,
            "S+0": 2000,
            "S+1": 2080,
            "S+2": 2120,
            "S+3": 2160,
            "S+4": 2200,
            "S+5": 2230,
            "S+6": 2260,
            "S+7": 2290,
            "S+8": 2320,
            "S+9": 2350,
        }.get(rank, None)
