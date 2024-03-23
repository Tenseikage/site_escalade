from passlib.context import CryptContext
password_ctx = CryptContext(schemes=['bcrypt']) # configuration de la bibliothèque
mdp = 'alexpass123'
hashed_psw =password_ctx.hash(mdp)
print(hashed_psw)
print(password_ctx.verify(mdp,hashed_psw))
