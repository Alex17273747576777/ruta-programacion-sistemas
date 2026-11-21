"""Laboratorio · Controlador PID discreto con anti-windup y planta de primer orden."""
from __future__ import annotations


def simular_pid(
    setpoint: float,
    kp: float,
    ki: float,
    kd: float,
    pasos: int = 80,
    dt: float = 0.1,
    salida_max: float = 100.0,
) -> list[float]:
    """Simula una planta térmica/velocidad discreta bajo control PID acotado."""
    y = 0.0
    integral = 0.0
    error_prev = setpoint - y
    traza: list[float] = []

    for _ in range(pasos):
        error = setpoint - y
        derivada = (error - error_prev) / dt
        integral_cand = integral + error * dt
        u_crudo = kp * error + ki * integral_cand + kd * derivada

        # Anti-windup: limita salida y solo acumula integral si no satura en la misma dirección.
        if u_crudo > salida_max:
            u = salida_max
            if error < 0:
                integral = integral_cand
        elif u_crudo < -salida_max:
            u = -salida_max
            if error > 0:
                integral = integral_cand
        else:
            u = u_crudo
            integral = integral_cand

        # Planta discreta de primer orden: y[k+1] = y[k] + dt * (-0.5 * y[k] + 0.5 * u)
        y = y + dt * (-0.5 * y + 0.5 * u)
        error_prev = error
        traza.append(round(y, 4))
    return traza
