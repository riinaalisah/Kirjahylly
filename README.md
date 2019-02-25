## Kirjahylly

Kirjahyllysovellukseen rekisteröidytään sähköpostin avulla. Kun sivuille on rekisteröitynyt, pystyy sen avulla hallitsemaan omia kirjoja erilaisin toiminnoin

  - kirjojen ja kirjailijoiden lisääminen tietokantaan
  - tietokantaan lisättyjen kirjojen lisääminen omaan hyllyyn ja sieltä poistaminen
  - tietokantaan lisättyjen kirjojen selaaminen
  - kirjojen merkitseminen luetuiksi tai lukemattomiksi
  - omien käyttäjätietojen päivittäminen
  
  
Nämä toiminnot ovat kaikille tavallisille käyttäjille. Admin-käyttäjille on lisäksi mahdollisuus poistaa käyttäjiä, kirjoja ja kirjailijoita tietokannasta. 


Sovelluksen testausta varten on tunnus, johon pystyy kirjautumaan käyttäjätunnuksella "testi" ja salasanalla "testi". Myös admin-käyttäjä löytyy tunnuksella "admin" ja salasanalla "admin1".


##### Linkkejä

Sovelluksen löytää osoitteesta http://tsoha-kirjahylly.herokuapp.com/ 

[Sovelluksen tietokantakaavio](https://github.com/riinaalisah/Kirjahylly/blob/master/documentation/kirjahylly_tietokantakaavio.png)

[User storyt](https://github.com/riinaalisah/Kirjahylly/blob/master/documentation/user_stories.md)


##### Asennus- ja käyttöohje

1. Lataa sovelluksen zip-tiedosto
2. Pura paketti
3. Navigoi kansioon johon purit tiedoston
4. Luo virtuaaliympäristö komennolla `python3 -m venv venv`
5. Aktivoi sen jälkeen virtuaaliympäristö komennolla `source venv/bin/activate`
6. Päivitä pip komennolla `pip install --upgrade pip`
7. Asenna riippuvuudet komennolla `pip install -r requirements.txt`
8. Käynnistä sovellus komennolla `python3 run.py`
