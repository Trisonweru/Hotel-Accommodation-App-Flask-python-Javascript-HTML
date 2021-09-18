# Hotel Reservation App

- This app allows an individual to book a hotel listd in the app. It also has options like card pay and MPESA integration.

## Technologies

- Python
- Flask server
- Javascript
- HTML
- CSS

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
