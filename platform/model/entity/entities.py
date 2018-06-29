from pygame.sprite import Sprite
from pygame import Rect


class Entity(Sprite):
    """
    Base entity, all entities are sub-classes of this

    All entities possess positing (Rect) information.  Generally X,Y,W,H
    the base entity allows for loading of X,Y,W,H or a Rect object
    """
    def __init__(self, x=0, y=0, width=0, height=0, rect=None, *groups):
        super().__init__(*groups)
        if type(rect) is Rect:
            self.rect = rect
        else:
            self.rect = Rect(x, y, width, height)

    def move(self, pos):
        """
        Move the entity
        :param pos: tuple
        """
        self.rect.topleft = pos


class LivingEntity(Entity):
    """
    LivingEntity represents an entity that has health and can be in a living or dead state
    based on it's current health.
    """
    def __init__(self, health=1, max_health=1, *groups, **kwargs):
        super().__init__(*groups, **kwargs)
        self.health = health
        self.max_health = max_health

    def damage(self, amt):
        """
        Reduce health by amount
        :param amt: int/float
        """
        self.health -= amt
        self._check_hp_bounds()

    def heal(self, amt):
        """
        Increase health by amount
        :param amt: int/float
        """
        self.health += amt
        self._check_hp_bounds()

    def is_alive(self):
        """
        Is the entities health above zero
        :return: bool
        """
        return self.health > 0

    def _check_hp_bounds(self):
        """
        Keeps the entities health within 0 and max_health
        """
        if 0 > self.health:
            self.health = 0
        if self.health > self.max_health:
            self.health = self.max_health
