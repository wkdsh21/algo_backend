from app import db


class Stock(db.Model):
    idx=db.Column(db.Integer, primary_key=True)
    itemCode=db.Column(db.String(45), nullable=False)
    name=db.Column(db.String(45), nullable=False)
    nutrition=db.Column(db.Text, nullable=False)


# 예제

# class Form(db.Model):
#     formIdx = db.Column(db.Integer, primary_key=True)
#     presentation = db.relationship(
#         'Presentation', back_populates="form")
#     scriptonly = db.relationship(
#         'Scriptonly', back_populates="form")


# class Presentation(db.Model):
#     pptIdx = db.Column(db.Integer, primary_key=True)
#     formIdx = db.Column(db.Integer, db.ForeignKey(
#         'form.formIdx', ondelete='CASCADE'))
#     form = db.relationship(
#         'Form', back_populates="presentation")
#     image = db.relationship(
#         'Image', back_populates="presentation")


# class Scriptonly(db.Model):
#     scriptOnlyIdx = db.Column(db.Integer, primary_key=True)
#     formIdx = db.Column(db.Integer, db.ForeignKey(
#         'form.formIdx', ondelete='CASCADE'))
#     form = db.relationship(
#         'Form', back_populates="scriptonly")
#     keyword = db.relationship(
#         'Keyword', back_populates="scriptonly")
#     script = db.Column(db.Text, nullable=False)


# class Image(db.Model):
#     imgIdx = db.Column(db.Integer, primary_key=True)
#     pptIdx = db.Column(db.Integer, db.ForeignKey(
#         'presentation.pptIdx', ondelete='CASCADE'))
#     presentation = db.relationship(
#         'Presentation', back_populates="image")
#     keyword = db.relationship(
#         'Keyword', back_populates="image")
#     pgNum = db.Column(db.Integer, nullable=False)
#     imgUrl = db.Column(db.Text, nullable=False)
#     script = db.Column(db.Text)
#     topic = db.Column(db.Integer)


# class Keyword(db.Model):
#     keyIdx = db.Column(db.Integer, primary_key=True)
#     keyword = db.Column(db.String(45), nullable=False)
#     imgIdx = db.Column(db.Integer, db.ForeignKey(
#         'image.imgIdx', ondelete='CASCADE'))
#     image = db.relationship(
#         'Image', back_populates="keyword")
#     # 0 :default , 1 :중요도1 , 2 :중요도2
#     level = db.Column(db.Integer, nullable=False, default=0)
#     scriptOnlyIdx = db.Column(db.Integer, db.ForeignKey(
#         'scriptonly.scriptOnlyIdx', ondelete='CASCADE'))
#     scriptonly = db.relationship(
#         'Scriptonly', back_populates="keyword")
#     topic = db.Column(db.Integer)
