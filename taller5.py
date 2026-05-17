"""
T5 - Falla, defecto y error (interfaz de escritorio con Tkinter).

RF1: Registro con correo y contraseña.
RF2: Inicio de sesión con máximo 3 intentos.

El código incluye defectos intencionales para evidenciar los conceptos:
- Error: equivocación humana al programar.
- Defecto: error plasmado en el código.
- Fallo: comportamiento incorrecto visible al usar la aplicación.
"""

import tkinter as tk


class ModuloAutenticacion:
    def __init__(self):
        self.usuarios = {}
        self.intentos = {}

    def registrar(self, correo, contrasena):
        # ERROR HUMANO 1:
        # Suponer que un correo válido siempre termina en ".com".
        # DEFECTO 1:
        # Regla de validación incompleta que rechaza correos válidos (.edu, .org, .co...).
        # FALLO 1:
        # Un visitante con correo real "ana@universidad.edu" no puede registrarse.
        if "@" not in correo or not correo.endswith(".com"):
            return False, "Correo inválido (defecto intencional: solo .com)."

        # ERROR HUMANO 2:
        # Guardar la contraseña forzándola a minúsculas.
        # DEFECTO 2:
        # Se pierde la diferencia entre mayúsculas/minúsculas.
        # FALLO 2:
        # El sistema puede aceptar como correcta una contraseña con otra capitalización.
        self.usuarios[correo] = contrasena.lower()
        self.intentos[correo] = 3
        return True, "Usuario registrado correctamente."

    def iniciar_sesion(self, correo, contrasena):
        if correo not in self.usuarios:
            return False, "El usuario no existe.", None

        if self.intentos.get(correo, 3) == 0:
            return False, "Acceso bloqueado: ya usaste los 3 intentos.", 0

        # Comparación intencionalmente defectuosa por el defecto 2.
        if self.usuarios[correo] == contrasena.lower():
            self.intentos[correo] = 3
            return True, "Inicio de sesión exitoso.", 3

        self.intentos[correo] -= 1
        restantes = self.intentos[correo]
        if restantes == 0:
            return False, "Acceso denegado: alcanzaste 3 intentos.", 0
        return False, f"Credenciales incorrectas. Intentos restantes: {restantes}.", restantes


class InterfazAutenticacion:
    def __init__(self, raiz):
        self.auth = ModuloAutenticacion()
        self.raiz = raiz
        self.raiz.title("T5 - Registro e Inicio de Sesión")
        self.raiz.geometry("540x330")

        tk.Label(raiz, text="Correo:").pack(pady=(12, 2))
        self.entrada_correo = tk.Entry(raiz, width=45)
        self.entrada_correo.pack()

        tk.Label(raiz, text="Contraseña:").pack(pady=(8, 2))
        self.entrada_contrasena = tk.Entry(raiz, width=45, show="*")
        self.entrada_contrasena.pack()

        marco_botones = tk.Frame(raiz)
        marco_botones.pack(pady=12)

        tk.Button(marco_botones, text="Registrar", width=14, command=self.registrar).grid(
            row=0, column=0, padx=4
        )
        tk.Button(
            marco_botones,
            text="Iniciar sesión",
            width=14,
            command=self.iniciar_sesion,
        ).grid(row=0, column=1, padx=4)
        tk.Button(marco_botones, text="Demo fallos", width=14, command=self.demo_fallos).grid(
            row=0, column=2, padx=4
        )

        self.estado = tk.Label(raiz, text="Listo.", fg="blue")
        self.estado.pack()

        self.salida = tk.Text(raiz, width=62, height=9, state="disabled")
        self.salida.pack(pady=8)

    def _leer_campos(self):
        correo = self.entrada_correo.get().strip()
        contrasena = self.entrada_contrasena.get()
        return correo, contrasena

    def _escribir_log(self, texto):
        self.salida.config(state="normal")
        self.salida.insert("end", texto + "\n")
        self.salida.see("end")
        self.salida.config(state="disabled")

    def registrar(self):
        correo, contrasena = self._leer_campos()
        ok, mensaje = self.auth.registrar(correo, contrasena)
        self.estado.config(text=mensaje, fg="green" if ok else "red")
        self._escribir_log(f"[REGISTRO] {correo} -> {mensaje}")

    def iniciar_sesion(self):
        correo, contrasena = self._leer_campos()
        ok, mensaje, _ = self.auth.iniciar_sesion(correo, contrasena)
        self.estado.config(text=mensaje, fg="green" if ok else "red")
        self._escribir_log(f"[LOGIN] {correo} -> {mensaje}")

    def demo_fallos(self):
        ok1, msj1 = self.auth.registrar("ana@universidad.edu", "ClaveSegura123")
        self._escribir_log(f"[DEMO FALLO 1] Registro .edu -> {ok1}, {msj1}")

        self.auth.registrar("carlos@gmail.com", "MiClaveSecreta")
        ok2, msj2, _ = self.auth.iniciar_sesion("carlos@gmail.com", "miclavesecreta")
        self._escribir_log(f"[DEMO FALLO 2] Login cambio mayúsculas -> {ok2}, {msj2}")
        self.estado.config(text="Demo de fallos ejecutada.", fg="purple")


if __name__ == "__main__":
    ventana = tk.Tk()
    InterfazAutenticacion(ventana)
    ventana.mainloop()
