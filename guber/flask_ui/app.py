from flask import Flask, render_template, request, redirect, url_for, flash
from form import DataForm
from validation import validate
import pandas as pd
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'AB089E9537733F10'

@app.route('/', methods=("POST", "GET"))
def main():
    form = DataForm()
    
    df = pd.read_excel('subset2_forkevin.xlsx')
    # get last 5 rows of the data frame where the Policy? column is not nan in reverse order
    row_data = df[df['Policy?'].notnull()].tail().values.tolist()[::-1]
    # get Snippets value and row number of first row where Policy? column is nan
    row_num = str(df[df['Policy?'].isnull()].index[0])
    snippet = df.iloc[int(row_num)]['Snippets']

    if form.is_submitted():
        if form.submit.data:
            # get the value of the Policy? column
            policy = form.policy.data
            proposal = form.proposal.data
            risky = form.risky.data
            keywords = form.keywords.data

            if validate(policy, proposal, risky, keywords):
                # update the data frame with the values
                df.at[int(row_num), 'Policy?'] = policy
                df.at[int(row_num), 'Proposal/Past?'] = proposal
                df.at[int(row_num), 'Risky/Not-Risky?'] = risky
                df.at[int(row_num), 'Keywords'] = keywords
            else: 
                flash('Invalid input. Please try again.', 'danger')
        else:
            prev_row = int(row_num) - 1
            df.at[prev_row, 'Policy?'] = None
            df.at[prev_row, 'Proposal/Past?'] = None
            df.at[prev_row, 'Risky/Not-Risky?'] = None
            df.at[prev_row, 'Keywords'] = None
                
        # save the updated data frame to the excel file
        df.to_excel('subset2_forkevin.xlsx', index=False)
        return redirect(url_for('main'))

    return render_template('main.html', column_names=df.columns.values, row_num=row_num, snippet=snippet, row_data=row_data, form=form)

if __name__ == "__main__":
    app.run(debug=True)