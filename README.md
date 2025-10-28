# Team-9 Backend
The Backend service for the [Team-9 Frontend](https://github.com/Agile-Software-Engineering-25/team-9-frontend-stammdaten-studieneinheiten)

## Features
- create course templates and instances
- create module templates and instances
- ...  
**TODO**

## Prerequisites
- [UV](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2): Modern Python Package Manager

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/Agile-Software-Engineering-25/team-9-backend-stammdaten-studieneinheiten.git
cd team-9-backend-stammdaten-studieneinheiten
```

### Install Dependencies
```bash
uv sync
```


### Run the Service
If it did't happen automatically already, activate the virtual environment (Indicated by the environment name in brackets before the path in your shell):
#### Windows
```powershell
PS> .venv\Scripts\activate
```
#### Linux and macOS
```bash
source .venv/bin/activate
```

**Now run the service with one of the following commands:**
- ` uvicorn app.main:app --reload `  
- `uv run uvicorn app.main:app --reload`
- `python -m uvicorn app.main:app --reload`
- `make run`
- `.\dev.ps1`

The service is now available on Port 8000 by default. Use the `--port` option to specify a different port.

FastAPI automatically generates a Swagger Documentation under `/docs/`

## Database Migration
Migration happens automatically when the app starts.  
If you make any changes to the database schema, you have to create a new database revision for the changes to appear in the app.

Create a new revision by running: ``.\create_migration.ps1`` in a terminal. You will be asked to give it a name.

Any app start from now on will also apply this migration, therefore adding your changes to the database.

## Testing
### Unit Tests
Unit Tests are defined in `/tests/`. 

To run all Unit-Tests make sure your packets are synced (`uv sync`) and your environment is activated ([see here](#windows)).  
Then run:
```bash
pytest
```

## Code Style & Linting
If you are using VS-Code as your text editor of choice, you can install the following extensions to make development easier:
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

### Settings for Ruff linter
You can configure special settings for your workspace in VS-Code with a `.vscode/settings.json` file. Add the following contents to that file:
```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
  }
}
```

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/learn/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/index.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [UV Documentation](https://docs.astral.sh/uv/)
