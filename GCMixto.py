# Generador Congruencial Mixto:
# Devuelve el primer valor generado y la semilla es fija (de momento)
# Comentario en una sola linea, Lo que este x debajo de este no cuenta

class GenCongruencialMixto:
    semilla = 0
    a_multiplicador = 5
    c_constante_aditiva = 7
    m_modulo = 8

    def N_i(self, aXi):
        return ((self.a_multiplicador * aXi) + self.c_constante_aditiva) % self.m_modulo

    def U_i(self):
        aXi = self.N_i(self.semilla)
        resultado = aXi / self.m_modulo
        self.semilla = aXi
        #if resultado != 0:
        return resultado
