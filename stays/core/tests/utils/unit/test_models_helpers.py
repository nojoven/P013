# Importations nécessaires pour les tests
from django.db import models

from core.utils.models_helpers import (BooleanFieldForeignKey,
                                       CharFieldForeignKey, ContentTypes,
                                       NullableBigIntegerFieldForeignKey,
                                       NullableIntegerFieldForeignKey,
                                       SlugFieldForeignKey,
                                       UUIDFieldForeignKey)


# Définition d'un modèle de test
class TestModel(models.Model):
    pass


# Test de la classe UUIDFieldForeignKey
def test_uuid_field_foreign_key():
    # Création d'une instance de UUIDFieldForeignKey
    uuid_field = UUIDFieldForeignKey(to=TestModel, on_delete=models.CASCADE)

    # Vérification que les attributs sont correctement initialisés
    assert uuid_field.db_column is None
    assert uuid_field.blank is True
    assert uuid_field.null is True


# Test de la classe CharFieldForeignKey
def test_char_field_foreign_key():
    # Création d'une instance de CharFieldForeignKey
    char_field = CharFieldForeignKey(to=TestModel, on_delete=models.CASCADE)

    # Vérification que les attributs sont correctement initialisés
    assert char_field.db_column is None
    assert char_field.blank is True
    assert char_field.null is True
    assert char_field.max_length == 500


# Test de la classe SlugFieldForeignKey
def test_slug_field_foreign_key():
    # Création d'une instance de SlugFieldForeignKey
    slug_field = SlugFieldForeignKey(to=TestModel, on_delete=models.CASCADE)

    # Vérification que les attributs sont correctement initialisés
    assert slug_field.db_column is None
    assert slug_field.blank is True
    assert slug_field.null is True
    assert slug_field.max_length == 255


# Test de la classe NullableIntegerFieldForeignKey
def test_nullable_integer_field_foreign_key():
    # Création d'une instance de NullableIntegerFieldForeignKey
    nullable_integer_field = NullableIntegerFieldForeignKey(
        to=TestModel, on_delete=models.CASCADE
    )

    # Vérification que les attributs sont correctement initialisés
    assert nullable_integer_field.db_column is None
    assert nullable_integer_field.blank is True
    assert nullable_integer_field.null is True


# Test de la classe NullableBigIntegerFieldForeignKey
def test_nullable_big_integer_field_foreign_key():
    # Création d'une instance de NullableBigIntegerFieldForeignKey
    nullable_big_integer_field = NullableBigIntegerFieldForeignKey(
        to=TestModel, on_delete=models.CASCADE
    )

    # Vérification que les attributs sont correctement initialisés
    assert nullable_big_integer_field.db_column is None
    assert nullable_big_integer_field.blank is True
    assert nullable_big_integer_field.null is True


# Test de la classe BooleanFieldForeignKey
def test_boolean_field_foreign_key():
    # Création d'une instance de BooleanFieldForeignKey
    boolean_field = BooleanFieldForeignKey(to=TestModel, on_delete=models.CASCADE)

    # Vérification que les attributs sont correctement initialisés
    assert boolean_field.db_column is None
    assert boolean_field.blank is True
    assert boolean_field.null is True


# Test de la classe ContentTypes
def test_content_types():
    # Vérification que les valeurs de ContentTypes sont correctes
    assert ContentTypes.text.value == ("text", "text")
    assert ContentTypes.voice.value == ("voice", "voice")
