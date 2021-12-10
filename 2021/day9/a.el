#!/usr/bin/env emacs --script

(defun height-at (i j height-map)
  (cond
   ((< i 0) 999)
   ((< j 0) 999)
   ((>= i (length height-map)) 999)
   ((>= j (length (nth 0 height-map))) 999)
   ((nth j (nth i height-map)))))

(let ((height-map '())
      (total-risk 0)
      line
      row)
  (while (setq line
	       (ignore-errors (read-from-minibuffer "")))
    (push (string-to-list line) height-map))
  (setq height (length height-map))
  (setq width (length (nth 0 height-map)))
  (dotimes (i height)
    (dotimes (j width)
      (setq me (height-at i j height-map))
      (and
       (> (height-at (- i 1) j height-map) me)
       (> (height-at (+ i 1) j height-map) me)
       (> (height-at i (- j 1) height-map) me)
       (> (height-at i (+ j 1) height-map) me)
       (setq total-risk (+ total-risk (+ 1 (- me ?0)))))))
  (print total-risk))
