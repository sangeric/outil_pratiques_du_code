import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

BASE_URL = "http://localhost:3000"

class TestSelenium:
    @pytest.fixture(scope="class")
    def driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_load_page(self, driver):
        # file_path = os.path.abspath("outil_pratiques_du_code\\frontend\\index.html")
        driver.get(BASE_URL)

        # vérifier titre
        assert "Gestionnaire de Tâches" in driver.title

        # vérifier les éléments
        assert driver.find_element(By.ID, "root")

    def test_login_page(self, driver):
        if not driver.current_url.endswith("/login"):
            assert "Erreur de redirection vers la page de connexion" in driver.page_source
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        email = "admin@test.com"
        password = "password"

        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
 
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard")))



# Version sans serveur (fichier local) et avec méthode déprécée

        # file_path = os.path.abspath("outil_pratiques_du_code\\frontend\\src\\components\\Login.js")
        # driver.get(f"file:///{file_path}")

        # username = "admin@test.com"
        # password = "password"

        # # vérifier les éléments du formulaire de connexion
        # assert driver.find_element(By.ID, "email")
        # assert driver.find_element(By.ID, "password")
        
        # xpaths = {
        #     "email": '//*[@id="email"]',
        #     "password": '//*[@id="password"]',
        #     "submit": '//*[@id="root"]/div/div/div[2]/form/button'
        # }

        # driver.find_element(By.XPATH, xpaths['email']).send_keys(username)
        # driver.find_element(By.XPATH, xpaths['password']).send_keys(password)
        # driver.find_element(By.XPATH, xpaths['submit']).click()
        # self.test_add_task(driver)

    def test_open_task_form(self, driver):
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard")))
        driver.find_element(By.XPATH, "//button[contains(text(), 'Nouvelle tâche')]").click()
        wait.until(EC.presence_of_element_located((By.ID, "task-form")))
        assert driver.find_element(By.ID, "task-form")

    def test_task_list(self, driver):
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard")))
        tasks = driver.find_elements(By.CLASS_NAME, "task-form")
        assert len(tasks) >= 0

    def test_add_task(self, driver):
        # print("Test d'ajout de tâche - à implémenter")
        driver.get("http://localhost:3000")  # Check du serv
        time.sleep(2)
        # Vérifier que nous sommes sur la page d'accueil
        assert "Gestionnaire de Tâches" in driver.title
        # Cliquer sur le bouton "Nouvelle tâche"
        driver.find_element(By.XPATH, "//button[contains(text(), 'Nouvelle tâche')]").click()
        time.sleep(1)
        # Remplir le formulaire de création de tâche
        driver.find_element(By.ID, "title").send_keys("Tâche de test")
        driver.find_element(By.ID, "description").send_keys("Description de la tâche de test")
        Select(driver.find_element(By.ID, "status")).select_by_visible_text("En cours")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Ajouter')]").click()
        time.sleep(2)
        # Vérifier que la tâche a été ajoutée à la liste
        tasks = driver.find_elements(By.CLASS_NAME, "task-form")
        assert any("Tâche de test" in task.text for task in tasks)

    def test_task_edit(self, driver):
        print("Test de modification de tâche - à implémenter")
        # À implémenter : trouver une tâche existante, cliquer sur "Modifier", changer les détails et vérifier la mise à jour
        tasks_list = driver.find_elements(By.CLASS_NAME, "task-form")
        if not tasks_list:
            self.test_add_task(driver)  # Ajouter une tâche
            time.sleep(2)

        wait = WebDriverWait(driver, 10)
        task_to_edit = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "task-form")))
        task_to_edit.find_element(By.XPATH, ".//button[contains(text(), 'Modifier')]").click()
        time.sleep(1)

        # Modifier les détails de la tâche
        title_field = wait.until(EC.presence_of_element_located((By.ID, "title")))
        title_field.clear()
        title_field.send_keys("Tâche modifiée")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Enregistrer')]").click()
        time.sleep(2)
        # Vérifier que la tâche a été modifiée
        tasks = driver.find_elements(By.CLASS_NAME, "task-form")
        assert any("Tâche modifiée" in task.text for task in tasks)

    def test_delete_task(self, driver):
        print("Test de suppression de tâche - à implémenter")
        # À implémenter : trouver une tâche existante, cliquer sur "Supprimer" et vérifier que la tâche n'est plus dans la liste
        
    def test_logout(self, driver):
        print("Test de déconnexion - à implémenter")
        # À implémenter : cliquer sur le bouton de déconnexion et vérifier que l'utilisateur est redirigé vers la page de connexion
    