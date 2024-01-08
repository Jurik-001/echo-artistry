Helper functions and Constants
==============================

The ``helper`` module in EchoArtistry provides utility functions and constants that are used throughout the application. It includes functions for file operations, logging configurations, and cost calculation constants for various AI models.

.. module:: echo_artistry.utils.helper
   :synopsis: Utility functions and constants for EchoArtistry.

Constants
---------

.. py:data:: MODEL_TOKEN_LENGTH_MAPPING
   :annotation: = {...}

   Mapping of model names to their token length and cost. The mapping includes models like 'gpt-3.5-turbo-1106', 'gpt-4', etc.

.. py:data:: IMAGE_CHARACTER_LENGTH_MAPPING
   :annotation: = {...}

   Defines the character length and cost per image for different image models like 'dall-e-2' and 'dall-e-3'.

.. py:data:: DEFAULT_MODEL_NAME
   :annotation: = 'gpt-3.5-turbo-1106'

   The default model name used in the application.

.. py:data:: DEFAULT_IMAGE_MODEL_NAME
   :annotation: = 'dall-e-3'

   The default image model name.

.. py:data:: DEFAULT_IMAGE_SIZE
   :annotation: = '1792x1024'

   The default size for generated images.

.. py:data:: DEFAULT_IMAGE_QUALITY
   :annotation: = 'standard'

   The default quality setting for generated images.

.. py:data:: MAX_RETRIES
   :annotation: = 5

   The maximum number of retries for certain operations.

Functions
---------

.. autofunction:: write_text_to_file
.. autofunction:: get_text_from_file
