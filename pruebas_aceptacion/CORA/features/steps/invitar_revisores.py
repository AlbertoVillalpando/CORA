from selenium.common.exceptions import TimeoutException
from behave import when, given, then
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given(u'selecciono la conferencia "{conferencia}" presionando el boton Invitaciones')
def step_impl(context, conferencia):
    driver = context.driver

    try:
        # Esperar a que la tabla esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )
    except TimeoutException:
        raise Exception("No se encontró la tabla de conferencias.")

    try:
        # Buscar la fila que contenga el nombre exacto de la conferencia
        fila = driver.find_element(
            By.XPATH, f"//tr[td[normalize-space(text())='{conferencia}']]"
        )
        context.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", fila)
        sleep(1)

        # Dentro de esa fila, encontrar el botón "Editar conferencia"
        boton_editar = fila.find_element(
            By.XPATH, ".//a[contains(text(), 'Invitaciones')]"
        )
        boton_editar.click()

    except Exception as e:
        raise Exception(
            f"No se pudo seleccionar la conferencia para editar: {e}")


@given(
    u'selecciono del listado de revisores a "{nombre}" de apellido "{apellido}"')
def step_impl(context, nombre, apellido):
    nombre_completo = nombre + " " + apellido
    context.driver.find_element(By.NAME, 'autor').send_keys(nombre_completo)


@when(u'presiono el botón "Invitar"')
def step_impl(context):
    context.driver.find_element(
        By.XPATH,
        '/html/body/div/div/div/div/div/div[2]/div[1]/div/form/div[2]/button').click()


@then(
    u'el sistema muestra en el listado de autores invitados a "{nombre}" de apellido "{apellido}"')
def step_impl(context, nombre, apellido):
    driver = context.driver
    nombre_completo = f"{nombre} {apellido}"

    try:
        # Esperar a que la tabla esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )
    except TimeoutException:
        raise Exception("No se encontró la tabla de autores.")

    try:
        # Buscar la fila que contenga el nombre completo del autor
        fila = driver.find_element(
            By.XPATH, f"//tr[td[contains(normalize-space(.), '{nombre_completo}')]]")
        # Hacer scroll hasta la fila encontrada (opcional pero útil)
        context.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", fila)
        sleep(1)

    except Exception:
        raise AssertionError(
            f"No se encontró al autor '{nombre_completo}' en el listado de autores invitados.")
