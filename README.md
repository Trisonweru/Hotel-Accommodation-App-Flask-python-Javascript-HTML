# Hotel Reservation App

## Create & Populate Databasse

- Prior to running the application please delete the existing users.db database

### Windows Powershell

```Powershell
$env:FLASK_APP="application"
```

```Powershell
flask shell
```

```Flask Shell
import application
```

```Flask Shell
from application import db
```

```Flask Shell
db.create_all()
```

```Flask Shell
import populateDB
```

```Flask Shell
exit()
```

### Unix

```Terminal
export FLASK_APP=application.py
```

```Terminal
flask shell
```

```Flask Shell
import application
```

```Flask Shell
from application import db
```

```Flask Shell
db.create_all()
```

```Flask Shell
import populateDB
```

```Flask Shell
exit()
```
