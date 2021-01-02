from typing import Optional
from typing import Tuple

from .notes import Note
from .notes import CHROMATIC_NOTES_FLATS
from .notes import CHROMATIC_NOTES_SHARPS
from .notes import FLAT_KEYS
from .notes import NATURAL_NOTES
from .notes import SHARP_KEYS


class NoteCollection:
    """
    Object to store and provide a basic setter for the root note of a note
    collection.
    """

    def __init__(self, root: Note):
        self._root = None
        self.set_root(root)

    @property
    def root(self) -> Note:
        return self._root

    def set_root(self, root: Note):
        """
        Ensure the root is a valid note. Subclasses extend with logic to set
        the root note.

        :param root: The root note for this scale.
        """
        if not isinstance(root, Note):
            msg = f'Root must be of type Note, not {type(root)}.'
            raise TypeError(msg)
        self._root = root


class ChromaticScale(NoteCollection):
    """
    An ascending chromatic scale starting with any natural, single sharp, or
    single flat note. No double sharps or flats are accounted for.
    """

    def __init__(self,
                 root: Optional[Note] = Note.C,
                 sharps: Optional[bool] = False):
        """
        Initialize scale. Silently overrides incorrect assignments to `sharps`
        e.g.::

            # F is a flat key
            scale = ChromaticScale(root=Note.F, sharps=True)
            assert scale.using_sharps is True


        :param root: The root note to use for the chromatic scale.
        :param sharps:
        """
        super().__init__(root)
        self._sharps = None
        self.update_sharps(sharps)

    def set_root(self, root: Note):
        """
        Extends NoteCollection's set_root() to update sharps any time the root is
        changed.

        :param root: The root note to use for this scale.
        """
        super().set_root(root)
        self.update_sharps()

    @property
    def sharps(self) -> bool:
        return self._sharps

    def update_sharps(self, sharps: Optional[bool] = None):
        """
        Set self._sharps based on the input and the root note of the scale.

        Automatically assigns self._sharps if `sharps` conflicts with the root
        note e.g. if the root is a flat key note such as F and sharps is set to
        True. Default for natural root notes is True.

        :param sharps: Whether or not to use sharps for this scale. If False,
            will use flats.
        """
        if self.root in SHARP_KEYS.difference(NATURAL_NOTES):
            sharps = True
        elif self.root in FLAT_KEYS.difference(NATURAL_NOTES):
            sharps = False
        elif self.root in NATURAL_NOTES:
            if sharps is not None:
                sharps = sharps
            else:
                sharps = True
        else:
            msg = f'Root must be a value in {list(Note)}. Not {self.root}'
            raise RuntimeError(msg)
        self._sharps = sharps

    def scale(self) -> Tuple[Note]:
        if self.sharps:
            return self._get_scale_with_sharps()
        return self._get_scale_with_flats()

    def use_sharps(self):
        """
        Try to set `self.sharps` to True. See the sharps setter for more
        information.
        """
        self.update_sharps(True)

    def use_flats(self):
        """
        Try to set `self.sharps` to False. See the sharps setter for more
        information.
        """
        self.update_sharps(False)

    def _get_scale_with_sharps(self) -> Tuple[Note]:
        """
        Return a chromatic scale of only sharp variations of notes starting with
        self.root.
        """
        if self.root in FLAT_KEYS:
            msg = f'The scale root must belong to a sharp key in order to' \
                  f' produce a scale with sharp notes, not {self.root}.'
            raise RuntimeError(msg)
        notes = CHROMATIC_NOTES_SHARPS
        root_idx = notes.index(self.root)
        return notes[root_idx:] + notes[:root_idx]

    def _get_scale_with_flats(self) -> Tuple[Note]:
        """
        Return a chromatic scale of only flat variations of notes starting with
        self.root.
        """
        if self.root in SHARP_KEYS:
            msg = f'The scale root must belong to a flat key in order to' \
                  f' produce a scale with flat notes, not {self.root}.'
            raise RuntimeError(msg)
        notes = CHROMATIC_NOTES_FLATS
        root_idx = notes.index(self.root)
        return notes[root_idx:] + notes[:root_idx]
