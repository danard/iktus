using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IktusApp.Models
{
  public record ECG
  (
    DateTime Date,
    FileInfo CSVFile,

    // Fitbit or AppleWatch
    string Type
  );
}
