def generate_signal(
    trend,
    phase,
    bos,
    choch
):

    confidence = 50

    # Tendencia

    if trend == "ALCISTA":
        confidence += 15

    elif trend == "BAJISTA":
        confidence += 15

    # Fase

    if phase == "IMPULSO":
        confidence += 15

    elif phase == "RETROCESO":
        confidence += 10

    # BOS

    if bos:
        confidence += 10

    # CHOCH

    if choch:
        confidence += 10

    # Señal

    if trend == "ALCISTA":

        signal = "COMPRAR"

    elif trend == "BAJISTA":

        signal = "VENDER"

    else:

        signal = "NO ENTRAR"

    return signal, confidence