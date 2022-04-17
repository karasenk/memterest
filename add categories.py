from data.category import Category
from data.db_session import create_session, global_init

names = ['про котиков', 'про собачек', 'про программистов',
         'про химиков', 'про художников', 'про наркоманов',
         'про Штирлица', 'не определено']

global_init("db/memterest.db")
db_sess = create_session()
for i in range(8):
    category = Category()
    category.name = names[i]
    db_sess.add(category)
    db_sess.commit()