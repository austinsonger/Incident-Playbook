import * as _ from 'lodash';

export function snakeToSpaced(word: string): string {
    return _.split(word, "_")
        .map(s => {
            if (s.length > 1) {
                const [first, ...rest] = Array.from(s);
                return [first.toUpperCase(), ...rest].join("");
            } else {
                return s.toUpperCase();
            }
        })
        .join(" ");
}
