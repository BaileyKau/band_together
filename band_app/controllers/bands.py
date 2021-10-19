from flask import render_template, redirect, session, request
from band_app import app
from band_app.models.user import User
from band_app.models.band import Band


#----------------Display Methods------------------#
@app.route("/my_band")
def my_bands():
    if 'user_id' not in session:
            return redirect("/")
    user = {
        "id": session['user_id']
    }
    return render_template('mybands.html', user=User.user_by_id(user), band_list=Band.get_all_bands(), joined_bands=Band.get_joined_bands(user))


@app.route("/band/new")
def new():
    if 'user_id' not in session:
            return redirect("/")
    user = {
        "id": session['user_id'],
    }
    return render_template('new_band.html', user=User.user_by_id(user))


@app.route("/band/edit/<int:id>")
def edit(id):
    if 'user_id' not in session:
            return redirect("/")
    data = {
        'id': id
    }
    user = {
        "id": session['user_id'],
    }
    return render_template('edit_band.html', user=User.user_by_id(user), band=Band.get_band(data))


#----------------Action Methods--------------------#
@app.route("/edit_band/<int:id>", methods=['POST'])
def edit_band(id):
    if not Band.validate_band(request.form):
        return redirect(f"/band/edit/{id}")
    Band.update_band(request.form)
    return redirect("/dashboard")

@app.route("/new_band", methods=['POST'])
def new_band():
    if not Band.validate_band(request.form):
        return redirect("/band/new")
    Band.new_band(request.form)
    return redirect("/dashboard")

@app.route("/delete_band/<int:id>")
def delete_band(id):
    data = {
        'id': id
    }
    Band.delete_band(data)
    return redirect("/my_band")

@app.route("/join_band/<int:user_id>/<int:band_id>")
def join_band(user_id, band_id):
    data = {
        'user_id': user_id,
        'band_id': band_id
    }
    User.join_band(data)
    return redirect("/my_band")

@app.route("/quit_band/<int:user_id>/<int:band_id>")
def quit_band(user_id, band_id):
    data = {
        'user_id': user_id,
        'band_id': band_id
    }
    User.quit_band(data)
    return redirect("/my_band")