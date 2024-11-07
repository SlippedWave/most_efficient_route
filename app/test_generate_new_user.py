import bcrypt
from app.models.user import User
from flask_sqlalchemy import SQLAlchemy
from app.extensions.database import get_db_session


def test_create_user():
    # Create a new user instance
    newUser = User(
        USR_email='francisco.gonzalez6694@alumnos.udg.mx',
        USR_name='Christian de Jesus Maximiliano',
        USR_last_name='Barriga Buenrostro',
        USR_PER_permitId=1,
        USR_telephone='3328152559',
        USR_statusId=6,
        USR_address='Blvd. Marcelino García Barragán #1421, esq Calzada Olímpica, C.P. 44430, Guadalajara, Jalisco, México.'
    )
    newUser.set_password('admin000.')

    # Add user to the session and commit (you might want to use a test database)
    session = get_db_session()
    session.add(newUser)
    session.commit()

    # Verify the user was created
    created_user = session.query(User).filter_by(USR_email='francisco.gonzalez6694@alumnos.udg.mx').first()
    assert created_user is not None
    assert created_user.USR_name == 'Christian de Jesus Maximiliano'
