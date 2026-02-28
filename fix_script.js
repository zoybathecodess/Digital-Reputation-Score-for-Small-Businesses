const fs = require('fs');
let content = fs.readFileSync('ScoreShield.html', 'utf8');

// Check how many trustColor declarations exist now
let indices = [];
let idx = content.indexOf('const trustColor');
while (idx !== -1) {
  indices.push(idx);
  idx = content.indexOf('const trustColor', idx + 1);
}
console.log('Found trustColor declarations at positions:', indices);
console.log('Total declarations:', indices.length);

// Find and remove the first trustColor declaration (at position 3274)
// by removing the section from "// Trust Color Function" to "// Trust Label Function"
const search = `// Trust Color Function
const trustColor = (
(score) => {
  if (score >= 80) r
eturn "#10b981";
  if (score >= 60) r
eturn "#84cc16";
  if (score >= 40) r
eturn "#f59e0b";
  return "#ef4444";
};


// Trust Label Function`;

const replace = `// Trust Label Function`;

if (content.includes(search)) {
  content = content.replace(search, replace);
  fs.writeFileSync('ScoreShield.html', content, 'utf8');
  console.log('Fixed: Removed duplicate trustColor function');
} else {
  console.log('Pattern not found - trying alternate method');
  // Alternative: just remove from "// Trust Color Function" to the next "//"
  const altSearch = '// Trust Color Function';
  const altIdx = content.indexOf(altSearch);
  if (altIdx >= 0) {
    // Find "// Trust Label Function"
    const labelIdx = content.indexOf('// Trust Label Function', altIdx);
    if (labelIdx >= 0) {
      const newContent = content.substring(0, altIdx) + content.substring(labelIdx);
      fs.writeFileSync('ScoreShield.html', newContent, 'utf8');
      console.log('Fixed: Removed duplicate trustColor function (alternate method)');
    }
  }
}
