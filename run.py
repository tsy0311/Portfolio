from app import create_app, db
from app.models import User, Project, BlogPost, Contact
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'BlogPost': BlogPost, 'Contact': Contact}


if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> bf6a5ec5733d63bd77c238ab5cfff388bcdb4093
