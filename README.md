# eAbsentee: Absentee Ballot Request System

A web app built with Flask which allows users to submit applications for absentee ballots in the state of Virginia. Somebody who wants an absentee ballot can complete a web form, and eAbsentee will use their input to complete the state-sanctioned PDF and email it to the state registrar of their locality. eAbsentee is based off of and expands upon [Horatio](https://github.com/TrustTheVote-Project/horatio-client), the original online absentee ballot application.

Absentee ballot request forms may be submitted electronically in Virginia under the authority of [attorney general opinion #13-111](http://ag.virginia.gov/files/Opinions/2014/13-111_Hinshaw.pdf) and [approval of the State Board of Elections](https://elections.virginia.gov/Files/Media/Agendas/20150513Minutes.pdf). (p. 7, lines 189–215).

### How it Works

-   Creates JSON object from user input data
-   Uses `pdfrw` to populate a fillable PDF
-   Sends the PDF to the state registrar of the inputted locality
-   If the email bounces, it's sent to a fallback state email

## Development

-   Create a file called `keys.py` with the following format:

```python
GMAIL_SENDER_ADDRESS = 'eAbsentee@gmail.com'
GMAIL_SENDER_PASSWORD = '<PASSWORD>'
SECRET_KEY = '<SECRET KEY>'
```

-   Run `pipenv install`

-   Run `pipenv shell`

-   Run `python scheduled_tasks/email_bounceback.py`, and login to your GMAIL-enabled API account.

-   Run `export FLASK_ENV=development`

-   Run `flask run`
