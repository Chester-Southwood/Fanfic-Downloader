# Fanfic-Downloader

<dl>
  <dt>Function</dt>
  <dd>Download story from fanfiction.net through URL passed in command line.</dd>

  <dt>Specifics</dt>
  <dd>
    <ul>
      <li>
        Error Checks
        <ul>
          <li>
            Such as 404, non-story fanfic.net page, or non fanfic.net page.
          </li>
         </ul>
      </li>
      <li>
        Creates folder if not already exists within src directory called downloads.
        <ul>
          <li>
            Each story will be downloaded within their own directory titled their name.
          </li>
          <li>
            All chapter(s) will be downloaded as txt files within the title directory, along with a file containing the description and a zip folder of the directory itself.
          </li>
        </ul>
      </li>
    </ul>
  </dd>
</dl>

