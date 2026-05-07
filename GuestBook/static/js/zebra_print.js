/**
 * Zebra Browser Print — minimalna integracja z REST API.
 * Browser Print musi być zainstalowany i uruchomiony na tym komputerze.
 * Domyślny port: 9090 (HTTP).
 */

const ZebraPrint = (function () {
  const BASE = 'http://localhost:9090';

  async function getDefaultPrinter() {
    const r = await fetch(`${BASE}/default?type=printer`);
    if (!r.ok) throw new Error('Zebra Browser Print nie odpowiada (port 9090). Sprawdź czy usługa jest uruchomiona.');
    const device = await r.json();
    if (!device || !device.uid) throw new Error('Nie znaleziono domyślnej drukarki w Zebra Browser Print.');
    return device;
  }

  async function send(zpl) {
    const device = await getDefaultPrinter();
    const r = await fetch(`${BASE}/write`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ device: device, data: zpl }),
    });
    if (!r.ok) throw new Error(`Błąd zapisu do drukarki: HTTP ${r.status}`);
  }

  /**
   * Drukuje ZPL i wywołuje callback z wynikiem.
   * @param {string} zpl - surowy kod ZPL
   * @param {function} onSuccess - wywołane po sukcesie
   * @param {function} onError - wywołane z message błędu
   */
  function print(zpl, onSuccess, onError) {
    send(zpl)
      .then(() => { if (onSuccess) onSuccess(); })
      .catch(err => { if (onError) onError(err.message); });
  }

  return { print, send, getDefaultPrinter };
})();
