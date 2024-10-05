from app import create_app, db
from app.models import User, Project, BlogPost, Contact
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'BlogPost': BlogPost, 'Contact': Contact}


if __name__ == '__main__':
    app.run(debug=True)
