# Creating application with tcutils

## Configuration


### Loading configuration from file

```
from schemas.app_config import AppConfigSchema
from tcutils.config import Configuration
from tcutils.paths import get_path


def load_config(config_file_name: str, config_schema=AppConfigSchema) -> Configuration:
    """Load configuration from file.
    """
    return Configuration.load(config_file_name, config_schema)

config_file_path = get_path('./config.yaml')
config = load_config(config_file_path)

```


### Creating configuration schema


```
import marshmallow

class SettingsSchema(marshmallow.Schema):
    login = marshmallow.fields.Email()
    password = marshmallow.fields.String(validate=[marshmallow.validate.Length(min=5), marshmallow.validate.ContainsNoneOf('i')])
    host = marshmallow.fields.String()
    port = marshmallow.fields.Integer()
    ssl = marshmallow.fields.Bool()
    starttls = marshmallow.fields.Bool()

class AppConfigSchema(marshmallow.Schema):
    settings = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(),
        values=marshmallow.fields.Nested(SettingsSchema))
    db = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(),
        values=marshmallow.fields.Raw())
```


### 


```
```
