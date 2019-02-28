### Käyttöohje

Tässä käyttöohjeessa listataan kaikki sovelluksen näkymät ja kerrotaan, mitä kaikkia ominaisuuksia niihin sisältyy. 

###### Rekisteröidy
Sovellukseen pystyy rekisteröitymään. Rekisteröitymislomakkeeseen tulee syöttää nimimerkki (5-30 merkkiä),
 sähköpostiosoite (5-50 merkkiä), ja salasana (5-20 merkkiä). Syötetty salasana tulee syöttää uudelleen vahvistamista
  varten. Salasana kryptataan tietoturvan vuoksi. Sähköpostia käytetään (tällä hetkellä) vain tilanteessa,
   jossa käyttältä on unohtunut salasana, jolloin salasananvaihtolinkki lähetetään käyttäjän syöttämään
    sähköpostiosoitteeseen. Kaikki kentät ovat pakollisia, ja niitä pystyy päivittämään myöhemmin. Käyttäjälle astetaan
     rooliksi automaattisesti tavallisen käyttäjän rooli, joten admin-käyttäjät tulee asettaa tietokannan kautta.

###### Kirjaudu sisään
Kirjautumisnäkymässä käyttäjän tulee syöttää käyttäjänimi ja salasana. Jos salasana on unohtunut, pääsee linkistä
 *Unohditko salasanasi?* pyytämään salasananvaihtolinkkiä.
 
###### Unohditko salasanasi?
Käyttäjä pystyy pyytämään linkkiä salasananvaihtonäkymään syöttämällä käyttäjätiliin liitetyn sähköpostiosoitteen.
 Sähköpostiin lähetettävä linkki ohjaa käyttäjän näkymään, jossa hänen tulee syöttää uusi salasana ja vahvistaa se. 
 Salasana kryptataan.
 
###### Kirjat
Tällä sivulla listataan kaikki tietokantaan lisätyt kirjat kirjan nimen mukaan aakkosjärjestyksessä. 
Jos käyttäjä ei ole kirjautunut sisään, näkyy hänelle vain kirjan ja kirjailijan nimi, mutta kirjautuneena käyttäjä
 näkee myös painikkeen, josta hän voi lisätä kirjan omaan hyllyynsä (paitsi jos kirja on jo käyttäjän hyllyssä).
 Kirjan tai kirjailijan nimeä klikkaamalla pääsee tarkastelemaan kirjan tai kirjailijan tietoja. Admin-käyttäjille
 näkyy myös painike kirjan poistamiseen tietokannasta.
 
###### Kirjan tiedot
Kirjan tiedot -sivulla näkyy kaikki tiedot mitä kyseiselle kirjalle on lisätty: nimi, kirjailija, julkaisuvuosi, sivumäärä ja ISBN-koodi.
Jos jotain kohtaa ei ole lisätty, se näkyy tyhjänä. Kirjautuneet käyttäjät pääsevät muokkaamaan kirjan tietoja 
*Muokkaa tietoja* -painikkeesta, ja kirjailijan tietoihin pääsee klikkaamalla kirjailijan nimeä.
 
###### Kirjailijat
Tällä sivulla listataan kaikki tietokantaan lisätyt kirjailijat. Kirjautumattomille ja tavallisille käyttäjille
näytetään kirjailijan nimi ja kuinka monta kirjaa kullekin kirjailijalle on lisätty tietokantaan. Admin-käyttäjälle näkyy myös
 painike kirjailijan poistamiseen tietokannasta. Kirjailijan tietoja pääsee tarkastelemaan klikkaamalla kirjailijan
 nimeä.
 
###### Kirjailijan tiedot
Kirjailijan tiedot -näkymässä käyttäjälle näytetään milloin kirjailija on lisätty tietokantaan, kuinka monta kirjaa
 tälle on lisätty tietokantaan, sekä listaus kirjailijan kirjoista. Kirjautuneet käyttäjät pystyvät tästä näkymästä 
 lisäämään kirjailijan kirjoja omaan hyllyyn (jos ne eivät jo ole siellä) ja siirtymään Muokkaa kirjailijan tietoja -näkymään 
 *Muokkaa tietoja* -painikkeesta.

###### Lisää kirjailija
Uuden kirjailijan pääsee lisäämään yläpalkin kohdasta *Lisää kirjailija*. Kirjailijalle annetaan etunimi ja
 sukunimi. Kumpikaan näistä nimistä ei saa sisältää välilyöntejä. 

###### Lisää kirja
Uuden kirjan pystyy lisäämään siirtymällä yläpalkista kohtaan *Lisää kirja*. Kirjalle tulee valita kirjailija
 dropdown-listasta, ja jos kyseistä kirjailijaa ei ole vielä tietokannassa, tulee se käydä ensin lisäämässä
  kohdasta *Lisää kirjailija*. Kirjalle tulee myös antaa 1-30 merkkiä pitkä nimi. Muut kentät (julkaisuvuosi
  sivumäärä ja ISBN-koodi) ovat vapaaehtoisia, ja ne voi myös lisätä jälkeenpäin.

###### Omat kirjat
Tällä sivulla käyttäjä näkee kirjat, jotka hän on lisännyt omaan hyllyynsä. Käyttäjä näkee myös kaksi
 yhteenvetoa: paljonko käyttäjän hyllyssä on kirjoja yhteensä, ja kuinka monta kirjaa käyttäjä on merkinnyt
  luetuksi. Jokaisen kirjan kohdalla lukee kirjan ja kirjailijan nimi, joiden vieressä näkyvät painikkeet
   kirjan merkitsemiseen luetuksi tai lukemattomaksi ja kirjan poistamiseen omasta hyllystä. Tämä poisto ei
    poista kirjaa tietokannasta, vaan ainoastaan käyttäjän omasta hyllystä. 
    
###### Omat tiedot
Omat tiedot -sivulla kirjautunut käyttäjä näkee omat tietonsa (käyttäjänimen, sähköpostiosoitteen ja liittymispäivämäärän) ja 
pääsee muokkaamaan niitä *Muokkaa tietoja* -painikkeesta. 

###### Muokkaa omia tietoja
Tässä näkymässä käyttäjä pystyy vaihtamaan käyttäjänimensä ja/tai sähköpostiosoitteensa (molempia ei tarvitse 
vaihtaa kerralla). Tässäkin käyttäjänimen tulee olla 5-30 merkkiä pitkä ja sähköpostiosoitteen 5-50 merkkiä
 pitkä. Sivulla on myös linkki salasananvaihtonäkymään ja painike käyttäjätilin  (paitsi admin-käyttäjillä)
 , jotka ohjaavat omiin näkymiinsä.
  
###### Vaihda salasana
Salasanaa vaihtaessa käyttäjän tulee syöttää nykyinen salasana, uusi salasana ja vahvistaa tämä syötetty uusi salasana. 
Salasanojen täsmäävyys tarkistetaan ja uusi salasana kryptataan.

###### Poista käyttäjätili
Jos käyttäjä haluaa poistaa käyttäjätilinsä, hänet ohjataan tälle vahvistussivulle. Kun käyttäjä painaa 
painiketta *Kyllä, poista käyttäjätilini*, kaikki tiedot käyttäjästä poistetaan tietokannasta, eikä poistoa voi enää perua.

###### Käyttäjät
Admin-käyttäjille yläpalkissa näkyy myös *Käyttäjät*, josta pääsee tarkastelemaan sovellukseen rekisteröityneitä käyttäjiä,
 ja poistamaan heitä tarvittaessa. Jokaisen käyttäjän (paitsi admin-käyttäjien) kohdalla on painike *Poista käyttäjä*, 
 josta pääsee poistonäkymään. Tässäkin tapauksessa käyttäjän poistaa kaikki tämän tiedot tietokannasta. Admin-käyttäjiä
  ei voi poistaa, vaan se tulee tehdä tietokannan kautta. 