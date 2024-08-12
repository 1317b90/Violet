from sqlalchemy.orm import Session

from SQLService import Models, Schemas

from datetime import datetime
# --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表

def addUser(db: Session, data: Schemas.User):
    userdb = Models.userTable(**data.dict())
    db.add(userdb)
    db.commit()
    db.refresh(userdb)


# 查询用户
def getUser(db: Session,username):
    return db.get(Models.User, username)

# 查询所有用户
def getUsers(db: Session):
    pass

# 更新用户信息
def setUser(db: Session, data: Schemas.User):
    user = getUser(db, data.username)
    for key, value in data.dict(exclude_unset=True).items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)

# 删除用户
def delUser(db: Session, username: str):
    user = getUser(db,username)
    db.commit()


# --------- 项目表 --------- 项目表 --------- 项目表 --------- 项目表 --------- 项目表 --------- 项目表 --------- 项目表 --------- 项目表

# 新建项目，只有username，其他都为空
def addItem(db: Session, username: str):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")
    item = Models.Item(
        username=username,
        itemName="新建项目"+now_str
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 根据项目id查询项目
def getItem(db: Session,id:int):
    return db.get(Models.Item, id)

# 查询指定用户的所有项目
def getItems_by_user(db: Session, username: str):
    return db.query(Models.Item).filter(Models.Item.username == username).all()

# 更新项目的公司基本资料
def setItemCompany(db: Session, data: Schemas.ItemCompany):
    item = getItem(db, data.id)
    for key, value in data.dict(exclude_unset=True).items():
        if hasattr(item, key):
            setattr(item, key, value)
    db.commit()
    db.refresh(item)

# 修改项目名称
def setItemName(db: Session,id:int, name:str):
    item = getItem(db, id)
    item.itemName = name
    db.commit()
    db.refresh(item)

# 删除项目
def delItem(db: Session, id: int):
    item = getItem(db, id)
    db.delete(item)
    db.commit()

# --------- 记录表 --------- 记录表 --------- 记录表 --------- 记录表 --------- 记录表 --------- 记录表


# 新增记录
def addLogr(db: Session, data: Schemas.Log):
    log = Models.Log(**data)
    db.add(log)
    db.commit()
    db.refresh(log)