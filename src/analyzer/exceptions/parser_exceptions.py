class ParserError(Exception):
    """Parser işlemleri için temel hata sınıfı."""


class InvalidFileError(ParserError):
    """Dosya beklenen formatta değil."""


class MissingColumnError(ParserError):
    """Beklenen sütun bulunamadı."""