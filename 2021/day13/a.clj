(require '[clojure.string :as string])

(defn abs [n]
  (max n (- n)))

(defn axis-and-coord [line]
  (re-seq #"[xy]|\d+" line))

(defn fold-at [line coords]
  (let [[axis n] (axis-and-coord line)
        n (#(Integer/parseInt %) n)]
    (map (fn [[i j]]
           (if
             (= axis "x")
             [(- n (abs (- n i))) j]
             [i (- n (abs (- n j)))]))
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
  (let [grid (fold-at (first lines) coords)]
    (println (count (distinct grid)))))
