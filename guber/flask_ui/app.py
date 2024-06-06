from flask import Flask, render_template, request
from form import DataForm
import pandas as pd
app = Flask(__name__)

app.config['SECRET_KEY'] = 'AB089E9537733F10'

@app.route('/', methods=("POST", "GET"))
def main():
    df = pd.read_excel('subset2_forkevin.xlsx')
    form = DataForm()
    # get last 5 rows of the data frame where the Policy? column is not nan
    row_data = df[df['Policy?'].notnull()].tail().values.tolist()
    return render_template('main.html', column_names=df.columns.values, row_data=row_data, form=form)

if __name__ == "__main__":
    app.run(debug=True)