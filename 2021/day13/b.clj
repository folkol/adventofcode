(require '[clojure.string :as string])

(defn abs [n]
  (max n (- n)))

(defn in?
  [coll elm]
  (some #(= elm %) coll))

(defn coord-picker [picker grid]
  (+ 1
     (reduce
       max
       (for [coord grid] (picker coord)))))

(defn width [grid]
  (coord-picker first grid))

(defn height [grid]
  (coord-picker second grid))

(defn print-grid [grid]
  (let [width (width grid)
        height (height grid)]
    (dotimes [j height]
      (dotimes [i width]
        (print (if (in? grid [i j])
                 "#"
                 ".")))
      (println))))

(defn axis-and-coord [line]
  (re-seq #"[xy]|\d+" line))

(defn fold-coord [n coord]
  (- n (abs (- n coord))))

(defn fold-at-line [line coords]
  (let [[axis fold-line] (axis-and-coord line)
        n (#(Integer/parseInt %) fold-line)]
    (map (fn [[i j]]
           (if (= axis "x")
             [(fold-coord n i) j]
             [i (fold-coord n j)]))
         coords)))

(defn parse-coordinates [str-line]
  (->> (string/split str-line #"," )
       (map #(Integer/parseInt %))))

(defn read-until-blank []
  (take-while
    (complement string/blank?)
    (repeatedly read-line)))

(let [coords (vec (map parse-coordinates (read-until-blank)))
      lines (clojure.string/split-lines (slurp *in*))]
  (print-grid
    (loop [lines lines
           coords coords]
      (if lines
        (let [line (first lines)]
          (recur (next lines) (fold-at-line line coords)))
        coords))))
