const orden = [];

orden.push("1:sync-inicio");
setTimeout(() => {
  orden.push("4:macrotarea-timeout");
  console.log("EVENT_LOOP=" + orden.join(","));
}, 0);
Promise.resolve().then(() => {
  orden.push("3:microtarea-promise");
});
orden.push("2:sync-fin");
