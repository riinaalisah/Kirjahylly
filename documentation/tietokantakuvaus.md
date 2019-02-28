#### Kuvaus sovelluksen tietokannasta

![alt text](https://github.com/riinaalisah/Kirjahylly/blob/master/documentation/kirjahylly-tietokantakaavio(1).png)


Sovelluksen tietokannassa on viisi tietokantataulua: book, account, author, users_books ja authors_books.

###### book
- id: Kirjan id-tunnus. Käytetään tunnistamiseen. Pääavain.
- date_created: Kirjan luontipäivämäärä.
- name: Kirjan nimi, 5-30 merkkiä pitkä. Pakollinen.
- year: Kirjan julkaisuvuosi. Korkeintaan 4 merkkiä. Ei pakollinen.
- pages: Kirjan sivumäärä. Korkeintaan 4 merkkiä. Ei pakollinen.
- isbn: Kirjan ISBN-koodi. Korkeintaan 19 merkkiä. Ei pakollinen.

###### account
- id: Käyttäjän id-tunnus. Käytetään tunnistamiseen. Pääavain.
- date_created: Käyttäjän luontipäivämäärä
- username: Käyttäjänimi. Käytetään kirjautumiseen. 5-30 merkkiä. Pakollinen.
- email: Sähköpostiosoite. Käytetään unohtuneen salasanan vaihtamiseen. 5-50 merkkiä. Pakollinen.
- password: Salasana. Käytetään kirjautumiseen. 5-20 merkkiä. Kryptataan. Pakollinen.
- role: Käyttäjän rooli. Oletuksena 'user', tietokannan kautta voi asettaa 'admin'. Pakollinen.

###### author
- id: Kirjailijan id-tunnus. Käytetään tunnistamiseen. Pääavain.
- date_created: Käyttäjän luontipäivämäärä.
- firstname: Kirjailijan etunimi. 1-30 merkkiä. Pakollinen.
- lastname: Kirjailijan sukunimi. 1-30 merkkiä. Pakollinen.

###### users_books

Tämä taulu yhdistää kirjat käyttäjiin: käyttäjällä voi olla useita kirjoja omassa hyllyssä, ja sama kirja voi olla usean käyttäjän hyllyssä.
- book_id: Kirjan id. Viiteavain kirjaan.
- user_id: Käyttäjän id. Viiteavain käyttäjään.
- read: status siitä, onko käyttäjä lukenut kirjan vai ei. Oletuksena false.

###### authors_books

Tämä taulu yhdistää kirjat kirjailijoihin: kirjailijalla voi olla useita kirjoja ja yhdellä kirjalla voi olla useita kirjailijoita (sovelluksen tämähetkinen toteutus tukee tosin vain yhtä kirjailijaa / kirja).
- book_id: Kirjan id. Viitevain kirjaan.
- author_id: Kirjailijan id. Viiteavain kirjailijaan.


---

Tietokannan CREATE TABLE-lauseet löytää [täältä].

[täältä]: https://github.com/riinaalisah/Kirjahylly/blob/master/documentation/create_table_lauseet
