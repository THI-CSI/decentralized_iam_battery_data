/**
 * Reports Core Web Vitals metrics to a provided callback.
 *
 * @remarks
 * This function dynamically imports the `web-vitals` library and hooks into
 * five performance metrics: CLS, INP, FCP, LCP, and TTFB.
 *
 * It only executes if a valid `onPerfEntry` callback function is provided.
 * This is typically used to log performance metrics to the console or send
 * them to an analytics backend.
 *
 * @param onPerfEntry - Optional callback function that receives performance entries.
 *
 * @example
 * ```ts
 * import reportWebVitals from './reportWebVitals';
 *
 * reportWebVitals(console.log);
 * ```
 */
const reportWebVitals = (onPerfEntry?: () => void) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ onCLS, onINP, onFCP, onLCP, onTTFB }) => {
      onCLS(onPerfEntry)
      onINP(onPerfEntry)
      onFCP(onPerfEntry)
      onLCP(onPerfEntry)
      onTTFB(onPerfEntry)
    })
  }
}

export default reportWebVitals
