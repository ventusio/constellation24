// Generate mock points and scatter them randomly
export const generateRandomPoints = (numPoints: number, center: [number, number], radius: number) => {
  const points: [number, number, number][] = [];
  for (let i = 0; i < numPoints; i++) {
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * radius;
    const lat = center[0] + (distance * Math.cos(angle)) / 111; // 1 degree latitude ~ 111 km
    const lng = center[1] + (distance * Math.sin(angle)) / (111 * Math.cos(center[0] * (Math.PI / 180))); // Adjust for longitude
    const intensity = Math.random();
    points.push([lat, lng, intensity]);
  }
  return points;
};
