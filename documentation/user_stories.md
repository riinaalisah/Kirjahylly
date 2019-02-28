## Käyttötapaukset

### Tavallinen käyttäjä

**"Uutena käyttäjänä pystyn rekisteröitymään sovellukseen, jotta pääsen hyödyntämään sen tarjoamia ominaisuuksia."**

- Uuden käyttäjän lisääminen: `INSERT INTO account (id, date_created, username, email, password, role) VALUES (1, CURRENT_DATE, 'myUsername', 'myEmail@email.com' 'myCryptedPassword', 'user');`

**"Käyttäjänä pystyn selaamaan tietokannan kirjoja, jotta pystyn löytämään uusia, minua kiinnostavia kirjoja."**

- Kirjojen listaus: `SELECT * FROM book;`

**"Käyttäjänä pystyn selaamaan tietokannan kirjailijoita, jotta näen keiden kirjailijoiden kirjoja muut käyttäjät lukevat."**

- Kirjailijoiden listaus: `SELECT * FROM author;`

**"Käyttäjän pystyn lisäämään kirjailijan tietokantaan, jotta voin lisätä kyseisen kirjailijan kirjan tietokantaan."**

- Kirjailijan lisääminen: `INSERT INTO author (id, date_created, firstname, lastname, books_count) VALUES (1, CURRENT_DATE, 'stephen', 'King', 0);`

**"Käyttäjänä pystyn muokkaamaan kirjailijan tietoja, jotta voin korjata niissä huomaamani virheet."**

- Kirjailijan tietojen muokkaus: `UPDATE author SET firstname='Stephen' WHERE id = 1;`

**"Käyttäjänä pystyn lisäämään uuden kirjan tietokantaan, jotta voin sitten lisätä sen omaan hyllyyni."**

- Kirjan lisääminen: `INSERT INTO book (id, date_created, name, year, pages, isbn) VALUES (1, CURRENT_DATE, 'MisEry', '1987', '410', '978-0-670-81364-3');`
- Kirjan liittäminen authors_books-tauluun: `INSERT INTO authors_books (book_id, author_id) VALUES (1, 1);`

**"Käyttäjänä pystyn muokkaamaan kirjan tietoja, jotta voin korjata niissä huomaamani virheet ja lisätä puuttuvia tietoja."**

- Kirjan tietojen muokkaus: `UPDATE book SET name = 'Misery', pages = '420' WHERE id = 1;`

**"Käyttäjän pystyn lisäämään kirjoja omaan hyllyyni, jotta pystyn seuraamaan omaa lukuharrastustani."**

- Kirjan liittäminen users_books-tauluun: `INSERT INTO users_books (book_id, user_id, read) VALUES (1, 1, 0);`

**"Käyttäjänä pystyn asettamaan kirjoja luetuiksi ja lukemattomiksi, jotta näen mitä kirjoja olen jo lukenut ja mitä on vielä lukematta."**

- Kirjan merkitseminen luetuksi: `UPDATE users_books SET read = 1 WHERE book_id = 1 AND user_id = 1;`
- Kirjan merkitseminen lukemattomaksi: `UPDATE users_books SET read = 0 WHERE book_id = 1 AND user_id = 1;`

**"Käyttäjänä pystyn poistamaan kirjoja omasta hyllystäni, jotta pystyn pitämään kirjalistani ajan tasalla."**

- Kirjan poistaminen käyttäjältä: `DELETE FROM users_books WHERE book_id=1 AND user_id = 1;`

**"Käyttäjänä pystyn näkemään tilastoja kirjoistani: kuinka paljon niitä on ja montako kirjaa olen lukenut."**

- Kaikkien kirjojen lukumäärä: `SELECT COUNT(users_books.book_id) FROM users_books WHERE user_id = 1;`

**"Käyttäjänä pystyn vaihtamaan salasanani, jos olen unohtanut sen."**

- Salasanan päivittäminen: `UPDATE account SET password = 'newCryptedPassword' WHERE id = 1;`

**"Käyttäjänä pystyn päivittämään käyttäjätietojani, jotta ne pysyvät ajan tasalla."**

- Käyttäjän tietojen päivittäminen: `UPDATE account SET username = 'myNewUsername', email = 'myNewEmail@email.com' WHERE id = 1;`


### Admin-käyttäjä

**"Admin-käyttäjänä pystyn poistamaan käyttäjiä, jotta käyttäjät pysyvät asiallisina."**

- Käyttäjän kirjojen poistaminen: `DELETE FROM users_books WHERE user_id = 1;`
- Käyttäjän poistaminen: `DELETE FROM account WHERE id = 1;`

**"Admin-käyttäjänä pystyn poistamaan kirjoja ja kirjailijoita, jotta tietokanta pysyy siistinä ja asiallisena."**

- Kirjan poistaminen
  - Kirjan poistaminen käyttäjiltä: `DELETE FROM users_books WHERE book_id = 1;`
  - Kirjan poistaminen kirjailijalta: `DELETE FROM authors_books WHERE book_id = 1;`
  - Kirjan poistaminen: `DELETE FROM book WHERE id = 1;`

- Kirjailijan poistaminen:
  1. Kirjailijan kirjojen nimien muuttaminen: `UPDATE book set name = 'delete' WHERE book.id IN (SELECT book_id FROM authors_books WHERE author_id = 1);`
  2. Kirjailijan ja kirjojen yhteyden poistaminen authors_books-taulusta: `DELETE FROM authors_books WHERE author_id = 1;`
  3. Käyttäjän ja kirjailijan kirjojen yhteyden poistaminen: `DELETE FROM users_books WHERE book_id in (SELECT id FROM book WHERE name = 'delete');`
  4. Kirjailijan poistaminen: `DELETE FROM author WHERE id = 1;`
  5. Kirjailijan kirjojen poistaminen: `DELETE FROM book WHERE name = 'delete';`
  - Tämä täytyy tehdä tässä järjestyksessä, sillä ainakin Heroku herjaa, jos esim. kirjan tai kirjailijan poistaa ennen kuin poistaa niiden yhteyden
  
